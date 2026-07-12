import AppLayout from "@/components/layout/AppLayout";
import AssetTable from "@/components/assets/AssetTable";

function AssetDirectoryPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Asset Directory
      </h1>

      <AssetTable />

    </AppLayout>
  );
}

export default AssetDirectoryPage;