import AppLayout from "@/components/layout/AppLayout";
import MaintenanceTable from "@/components/maintenance/MaintenanceTable";

function MaintenancePage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Maintenance
      </h1>

      <MaintenanceTable />

    </AppLayout>
  );
}

export default MaintenancePage;