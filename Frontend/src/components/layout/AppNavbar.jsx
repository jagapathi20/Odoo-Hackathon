import { SidebarTrigger } from "@/components/ui/sidebar";
import { Bell, Search } from "lucide-react";

function AppNavbar() {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-6">

      <div className="flex items-center gap-4">

        <SidebarTrigger />

        <h1 className="text-xl font-bold text-slate-800">
          AssetFlow
        </h1>

      </div>

      <div className="flex items-center gap-4">

        <div className="flex items-center gap-2 rounded-lg border px-3 py-2 bg-slate-50">

          <Search size={18} />

          <input
            type="text"
            placeholder="Search..."
            className="bg-transparent outline-none text-sm"
          />

        </div>

        <Bell className="cursor-pointer" />

        <div className="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-semibold">

          A

        </div>

      </div>

    </header>
  );
}

export default AppNavbar;