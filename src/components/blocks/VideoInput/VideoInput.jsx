import styles from "./VideoInput.module.css";

import { useState, useRef } from "react";
import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";

export default function VideoInput({ width, height }) {
  const inputRef = useRef();
  const [source, setSource] = useState();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    setSource(url);
  };

  const handleChoose = (e) => {
    inputRef.current.click();
  };

  return (
    <div className={styles.upload}>
      <input
        ref={inputRef}
        type="file"
        onChange={handleFileChange}
        accept=".mov,.mp4"
      />
      {!source && (
        <button onClick={handleChoose}>
          <UploadIcon width={200} height={200} />
        </button>
      )}
      {source && <video width="100%" height={height} controls src={source} />}
      <div className="footer">{source || "Nothing selectd"}</div>
    </div>
  );
}
