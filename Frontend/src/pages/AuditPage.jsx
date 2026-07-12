import AppLayout from "@/components/layout/AppLayout";
import AuditTable from "@/components/audits/AuditTable";

function AuditPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Asset Audits
      </h1>

      <AuditTable />

    </AppLayout>
  );
}

export default AuditPage;