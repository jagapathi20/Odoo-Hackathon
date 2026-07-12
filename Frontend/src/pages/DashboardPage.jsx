import AppLayout from "@/components/layout/AppLayout";

function DashboardPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-6">
        Dashboard
      </h1>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-slate-500">Assets</p>
          <h2 className="text-3xl font-bold mt-2">245</h2>
        </div>

        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-slate-500">Allocated</p>
          <h2 className="text-3xl font-bold mt-2">181</h2>
        </div>

        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-slate-500">Maintenance</p>
          <h2 className="text-3xl font-bold mt-2">12</h2>
        </div>

        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-slate-500">Bookings</p>
          <h2 className="text-3xl font-bold mt-2">36</h2>
        </div>

      </div>

    </AppLayout>
  );
}

export default DashboardPage;