import AppLayout from "@/components/layout/AppLayout";
import AllocationTable from "@/components/allocations/AllocationTable";

function AllocationPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Asset Allocation
      </h1>

      <AllocationTable />

    </AppLayout>
  );
}

export default AllocationPage;