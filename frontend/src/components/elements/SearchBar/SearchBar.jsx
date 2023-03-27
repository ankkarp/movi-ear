import SearchButton from "@/components/buttons/SearchButton/SearchButton";
import styles from "./SearchBar.module.css";

const SearchBar = () => {
  return (
    <div className={styles.searchcontainer}>
      <input type="text" className={styles.search} />
      <SearchButton />
    </div>
  );
};

export default SearchBar;
