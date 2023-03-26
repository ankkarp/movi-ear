import Header from "@/components/blocks/Header/Header";
import Head from "next/head";

const MainLayout = ({ children }) => {
  return (
    <>
      <Head>
        <title>MoviEar</title>
        <meta
          name="description"
          content="Аудиосопровождение для фильмов и видео | Главная страница"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        {/* <link rel="icon" href="/favicon.ico" /> */}
      </Head>
      <Header />
      {children}
    </>
  );
};

export default MainLayout;
