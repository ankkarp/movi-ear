import styles from "./VideoInput.module.css";

import { useState, useRef } from "react";
import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";
import http from "../../../api/http-common";
import Router from "next/router";
import LoadingIcon from "@/components/icons/LoadingIcon/LoadingIcon";
import Image from "next/image";

export default function VideoInput() {
  const [loading, setLoading] = useState(false);
  const inputRef = useRef();

  const redirectToVideo = (r) => {
    window.location = "/" + r.data.hash;
  };

  const handleFileChange = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    let formData = new FormData();
    formData.append("file", file);
    try {
      http
        .post("upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          // onUploadProgress,
        })
        .then((r) => redirectToVideo(r));
      setLoading(true);
    } catch (e) {
      console.log(e);
    }
  };

  const handleChoose = (e) => {
    inputRef.current.click();
  };

  return (
    <div className={styles.container}>
      <div className={styles.upload}>
        {loading ? (
          <LoadingIcon />
        ) : (
          <button onClick={handleChoose}>
            <input
              ref={inputRef}
              type="file"
              onChange={handleFileChange}
              disabled={loading}
              accept=".mov,.mp4,.webm,.wmv,.avi,.avchd,.flv,.f4v,.swf,.mkv,.html5,.mpg,.mpeg"
            />
            <UploadIcon width={200} height={200} />
            <div className="footer">Загрузите видео</div>
          </button>
        )}
      </div>
      {/* )} */}
    </div>
  );
}
