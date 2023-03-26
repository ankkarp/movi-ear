import UploadButton from "@/components/buttons/UploadButton/UploadButton";
import SearchBar from "@/components/elements/SearchBar/SearchBar";
import styles from "./Header.module.css";

const Header = () => {
  return (
    <div className={styles.header}>
      <SearchBar />
      <UploadButton />
    </div>
  );
};

export default Header;
