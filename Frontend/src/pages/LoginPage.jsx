import LoginForm from "@/features/auth/LoginForm";

function LoginPage() {
  return (
    <div className="min-h-screen grid grid-cols-12">

      <div className="col-span-3 bg-slate-900 text-white flex flex-col justify-between p-10">

        <div>

          <div className="w-12 h-12 rounded bg-yellow-500 mb-8"/>

          <h1 className="text-3xl font-bold">
            AssetFlow
          </h1>

          <p className="mt-2 text-slate-400">
            Smart Asset Management Platform
          </p>

        </div>

        <div className="space-y-3 text-slate-300">

          <p>✔ Asset Tracking</p>
          <p>✔ Booking</p>
          <p>✔ Maintenance</p>
          <p>✔ Reports</p>

        </div>

      </div>

      <div className="col-span-9 flex justify-center items-center bg-white">

        <LoginForm />

      </div>

    </div>
  );
}

export default LoginPage;