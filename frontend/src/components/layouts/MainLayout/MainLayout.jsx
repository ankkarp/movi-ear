import Header from "@/components/blocks/Header/Header";
import Head from "next/head";

const MainLayout = ({ children, show = true }) => {
  return (
    <>
      <Head>
        <title>MoviEar - Аудиосопровождение видео</title>
        <meta
          name="description"
          content="Аудиосопровождение для фильмов и видео"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/hearing.ico" />
      </Head>
      <Header show={show} />
      {children}
    </>
  );
};

export default MainLayout;
