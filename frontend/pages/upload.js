import VideoInput from "@/components/blocks/VideoInput/VideoInput";
import MainLayout from "@/components/layouts/MainLayout/MainLayout";
const upload = () => {
  return (
    <MainLayout show={false}>
      <VideoInput />
    </MainLayout>
  );
};
export default upload;
