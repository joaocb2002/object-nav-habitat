import random
import hydra
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
from hydra.utils import to_absolute_path
from objectnav.sim.agent import init_agent
from objectnav.sim.simulator import make_sim
from objectnav.sim.navmesh import compute_navmesh
from objectnav.sim.maps import build_grid_map_from_navmesh
from objectnav.utils.spatial.rotations import rotation_to_yaw
from objectnav.utils.visualization.maps import save_map_with_agent
from objectnav.utils.visualization.observations import save_rgbd_observations
from objectnav.utils.visualization.detections import save_yolo_detections_plot
from objectnav.perception.config import YoloConfig
from objectnav.perception.pipeline import build_yolo_detector, run_yolo_detections
from objectnav.config import DataAssetsConfig, load_objectnav_data_assets


@hydra.main(config_path="../configs", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:

    # Seed
    seed = cfg.get("seed")
    seed = random.randint(0, 2**32 - 1) if seed is None else int(seed)

    print("=== Effective config ===")
    print(OmegaConf.to_yaml(cfg))

    # To create artifacts, logs and checkpoints directories 
    output_dir = Path(to_absolute_path(cfg.paths.artifacts_dir)) # Artifacts
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load reproducibility data assets (camera intrinsics, classes, bins)
    data_assets_cfg = DataAssetsConfig.from_mapping(cfg.data_assets, resolve_path=to_absolute_path)
    data_assets = load_objectnav_data_assets(data_assets_cfg)
    print(
        "Loaded data assets:",
        f"{len(data_assets.indoor_classes)} classes,",
        f"{len(data_assets.object_class_bins)} bin tables,",
        f"resolution={data_assets.camera_intrinsics.width}x{data_assets.camera_intrinsics.height}",
    )

    # Load YOLO11x model from composed Hydra config
    yolo_config = YoloConfig.from_mapping(cfg.perception, resolve_path=to_absolute_path)
    yolo_detector = build_yolo_detector(yolo_config)

    # Launch simulator
    simulator = make_sim(
        scene_dataset_config=Path(to_absolute_path(cfg.sim.scene_dataset_config)),
        scene_id=str(cfg.sim.scene_id),
    )
        
    # Setting a seed for reproducibility    
    random.seed(seed) # This will make random sampling reproducible (eg. yaw degree)
    simulator.sim.seed(seed)
    simulator.sim.pathfinder.seed(seed)

    # Get navigation mesh
    if compute_navmesh(simulator.sim):
        grid_map = build_grid_map_from_navmesh(simulator.sim)
    else:
        raise RuntimeError("Failed to compute navigation mesh.")

    # Initialize the (only) agent: configuration was made in simulator creation
    agent = init_agent(simulator.sim)
    
    # Select action space
    action_names = list(simulator.cfg.agents[0].action_space.keys())

    # Random short rollout to test
    T = 10
    for i in range(T):

        print(f"\nStep {i+1} / {T}")
        action = random.choice(action_names)
        observations = simulator.sim.step(action)
        rgb, depth, collided = observations["color_sensor"], observations["depth_sensor"], observations["collided"]
        agent_state = agent.get_state()

        print("Action:", action)
        print("Collided:", collided)
        print("Agent_state: position", agent_state.position, "yaw", rotation_to_yaw(agent_state.rotation)) 
        save_rgbd_observations(rgb, depth, save_path=output_dir / f"observations_step_{i+1}.png")
        save_map_with_agent(
            grid_map,
            agent_state.position,
            agent_state.rotation,
            save_path=output_dir / f"grid_map_with_agent_step_{i+1}.png",
            sim=simulator.sim,
            title="Grid Map + Agent",
            agent_radius_px=20,
        )
        
        # RGB is a 4 channel image. Print the max, min and mean value of alpha
        alpha_channel = rgb[:, :, 3]
        print(f"Alpha channel - Max: {alpha_channel.max()}, (a < 255).mean(): {((alpha_channel < 255).mean())}")

        # Run YOLO. Our images are in RGB format, but YOLO expects BGR for numpy input
        detections, yolo_result = run_yolo_detections(yolo_detector,rgb,input_color="rgb")

        save_yolo_detections_plot(
            yolo_result,
            save_path=output_dir / f"detections_step_{i+1}.png",
            show_conf=True,
            show_labels=True,
            show_boxes=True,
        )

        print("Detections:")
        for det in detections:
            xyxy_fmt = "(" + ", ".join(f"{v:.2f}" for v in det.xyxy) + ")"
            probs_fmt = (
                "(" + ", ".join(f"{v:.3f}" for v in det.probs) + ")"
                if det.probs is not None
                else "N/A"
            )
            print(
                f"Class: {det.cls_name}, Confidence: {det.conf:.2f}, Box: {xyxy_fmt}, Scale: {det.scale:.2f},"
                f"\n Probs: {probs_fmt}"
            )


    # Close simulator
    print("Closing simulator...")
    simulator.close()
    

if __name__ == "__main__":
    main()