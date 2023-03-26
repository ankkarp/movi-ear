import styles from "./VideoInput.module.css";

import { useState, useRef } from "react";
import { FileUploader } from "react-drag-drop-files";
import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";

export default function VideoInput({ width, height }) {
  const fileTypes = ["MP4", "MOV"];
  const [source, setSource] = useState();

  const [file, setFile] = useState(null);
  const handleChange = (file) => {
    setFile(file);
    console.log(file);
    setSource(URL.createObjectURL(file));
  };

  return (
    <div className={styles.upload}>
      <FileUploader
        handleChange={handleChange}
        name="file"
        types={fileTypes}
        styles={{ color: "yellow" }}
      />
      <p>{file ? `Загружено: ${file.name}` : "Перетащите или выберите файл"}</p>
    </div>
  );
}
