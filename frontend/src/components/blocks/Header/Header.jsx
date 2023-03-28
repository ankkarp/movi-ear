import UploadButton from "@/components/buttons/UploadButton/UploadButton";
import SearchBar from "@/components/elements/SearchBar/SearchBar";
import styles from "./Header.module.css";

const Header = ({ show = true }) => {
  return (
    <div className={styles.header}>
      {/* <SearchBar /> */}
      <div />
      {show ? <UploadButton /> : <div />}
    </div>
  );
};

export default Header;
