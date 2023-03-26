import SearchIcon from "@/components/icons/SearchIcon/SearchIcon";
import styles from "./SearchButton.module.css";

const SearchButton = () => {
  return (
    <button className={styles.search}>
      <SearchIcon width="20" height="20" />
    </button>
  );
};

export default SearchButton;
