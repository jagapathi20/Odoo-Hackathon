import AppLayout from "@/components/layout/AppLayout";

import KPICard from "@/components/dashboard/KPICard";
import RecentActivity from "@/components/dashboard/RecentActivity";
import QuickActions from "@/components/dashboard/QuickActions";

function DashboardPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Dashboard
      </h1>

      <div className="grid lg:grid-cols-4 gap-6 mb-8">

        <KPICard
          title="Total Assets"
          value="245"
          color="text-blue-600"
        />

        <KPICard
          title="Allocated"
          value="181"
          color="text-green-600"
        />

        <KPICard
          title="Maintenance"
          value="12"
          color="text-red-600"
        />

        <KPICard
          title="Bookings"
          value="36"
          color="text-yellow-500"
        />

      </div>

      <div className="grid lg:grid-cols-3 gap-6">

        <div className="lg:col-span-2">

          <RecentActivity />

        </div>

        <QuickActions />

      </div>

    </AppLayout>
  );
}

export default DashboardPage;