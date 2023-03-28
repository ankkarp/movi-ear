import VideoPlayer from "@/components/blocks/VideoPlayer/VideoPlayer";
import MainLayout from "@/components/layouts/MainLayout/MainLayout";
import http from "../src/api/http-common";

const VideoPage = ({ hash }) => {
  return (
    <MainLayout>
      <VideoPlayer hash={hash} />
    </MainLayout>
  );
};

export async function getServerSideProps(context) {
  try {
    await http.get(`video/${context.params.hash}`);
  } catch (err) {
    return {
      notFound: true,
    };
  }
  // await fetch(`${process.env.SERVER}/video/${context.params.hash}`);
  const hash = context.params.hash;
  // console.log(`${process.env.SERVER}/video/${hash}`);
  return { props: { hash } };
}

export default VideoPage;
