import UploadIcon from "@/components/icons/UploadIcon/UploadIcon";
import Link from "next/link";

const UploadButton = () => {
  return (
    <Link href="/upload">
      <UploadIcon width="30" height="30" />
    </Link>
  );
};

export default UploadButton;
