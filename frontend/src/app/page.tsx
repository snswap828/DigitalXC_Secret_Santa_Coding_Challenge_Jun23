import UploadFiles from "@/features/upload-files";


export default function Home() {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10 align-center">
        <UploadFiles />
      </div>
    </div>
  );
}
