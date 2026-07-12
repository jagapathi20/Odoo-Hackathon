import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import AppNavbar from "./AppNavbar";
import AppSidebar from "./AppSidebar";

function AppLayout({ children }) {
  return (
    <SidebarProvider defaultOpen={true}>
      <AppSidebar />

      <SidebarInset className="min-h-screen bg-slate-100">
        <AppNavbar />

        <main className="p-6">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}

export default AppLayout;