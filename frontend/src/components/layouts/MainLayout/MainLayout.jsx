import Header from "@/components/blocks/Header/Header";
import Head from "next/head";
import { useEffect, useState } from "react";
import styles from "./MainLayout.module.css";

const MainLayout = ({ children, show = true }) => {
  const [active, setActive] = useState(false);

  useEffect(() => {
    setActive(true);
  }, []);

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
      <div className={`${styles.container} ${active ? styles.active : ""}`}>
        {children}
      </div>
    </>
  );
};

export default MainLayout;
