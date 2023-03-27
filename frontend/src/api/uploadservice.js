import http from "./http-common";

class UploadFilesService {
  upload(file) {
    let formData = new FormData();

    formData.append("file", file);

    console.log(formData);
    return http.post("upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      // onUploadProgress,
    });
  }

  getFiles() {
    return http.get("/files");
  }
}

export default new UploadFilesService();
