import styles from "./VideoPlayer.module.css";

const VideoPlayer = ({ hash }) => {
  return (
    <div className={styles.player}>
      <video
        controls="controls"
        autoPlay="autoplay"
        src={`${process.env.SERVER}/video/${hash}`}
      />
    </div>
  );
};

export default VideoPlayer;
