import AppLayout from "@/components/layout/AppLayout";
import DepartmentTable from "@/components/organization/DepartmentTable";
import CategoryTable from "@/components/organization/CategoryTable";
import EmployeeTable from "@/components/organization/EmployeeTable";

function OrgSetupPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Organization Setup
      </h1>

      <div className="space-y-8">

        <DepartmentTable />

        <CategoryTable />

        <EmployeeTable />

      </div>

    </AppLayout>
  );
}

export default OrgSetupPage;