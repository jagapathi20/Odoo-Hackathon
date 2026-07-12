import AppLayout from "@/components/layout/AppLayout";
import ReportCards from "@/components/reports/ReportCards";
import ReportCharts from "@/components/reports/ReportCharts";

function ReportsPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Reports & Analytics
      </h1>

      <ReportCards />

      <ReportCharts />

    </AppLayout>
  );
}

export default ReportsPage;