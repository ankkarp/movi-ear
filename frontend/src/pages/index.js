import { Inter } from "next/font/google";
import MainLayout from "@/components/layouts/UploadLayout/MainLayout";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return <MainLayout />;
}
