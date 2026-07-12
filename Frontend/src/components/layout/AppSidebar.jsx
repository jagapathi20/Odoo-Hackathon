import { Link, useLocation } from "react-router-dom";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

import { navigation } from "@/utils/navigation";

function AppSidebar() {
  const location = useLocation();

  return (
    <Sidebar className="border-r bg-white">

      <SidebarHeader className="border-b px-6 py-8">

        <div className="flex flex-col">

          <h1 className="text-4xl font-extrabold tracking-tight text-indigo-600">
            AssetFlow
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Asset Management
          </p>

        </div>

      </SidebarHeader>

      <SidebarContent className="px-3 py-5">

        <SidebarGroup>

          <SidebarGroupContent>

            <SidebarMenu className="space-y-2">

              {navigation.map((item) => {
                const Icon = item.icon;

                const active = location.pathname === item.path;

                return (
                  <SidebarMenuItem key={item.title}>

                    <SidebarMenuButton
                      asChild
                      isActive={active}
                      className={`
                        h-14 rounded-xl transition-all duration-200
                        ${active
                          ? "bg-indigo-50 text-indigo-600 font-semibold shadow-sm"
                          : "hover:bg-slate-100 hover:text-indigo-600"}
                      `}
                    >
                      <Link
                        to={item.path}
                        className="flex items-center gap-4 px-4"
                      >
                        <div
                          className={`
                            flex h-10 w-10 items-center justify-center rounded-xl
                            ${active ? "bg-indigo-100" : "bg-slate-100"}
                          `}
                        >
                          <Icon size={20} />
                        </div>

                        <span className="text-base">
                          {item.title}
                        </span>

                      </Link>

                    </SidebarMenuButton>

                  </SidebarMenuItem>
                );
              })}

            </SidebarMenu>

          </SidebarGroupContent>

        </SidebarGroup>

      </SidebarContent>

      <SidebarFooter className="border-t bg-slate-50 p-5">

        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center rounded-full bg-indigo-600 text-lg font-bold text-white">
            A
          </div>

          <div>

            <p className="font-semibold text-slate-800">
              Admin
            </p>

            <p className="text-sm text-slate-500">
              Asset Manager
            </p>

          </div>

        </div>

      </SidebarFooter>

    </Sidebar>
  );
}

export default AppSidebar;