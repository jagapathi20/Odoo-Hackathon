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
    <Sidebar>

      <SidebarHeader className="border-b h-16 flex items-center justify-center">

        <h1 className="text-2xl font-bold text-indigo-600">
          AssetFlow
        </h1>

      </SidebarHeader>

      <SidebarContent>

        <SidebarGroup>

          <SidebarGroupContent>

            <SidebarMenu>

              {navigation.map((item) => {
                const Icon = item.icon;

                return (
                  <SidebarMenuItem key={item.title}>

                    <SidebarMenuButton
                      asChild
                      isActive={location.pathname === item.path}
                    >
                      <Link to={item.path}>

                        <Icon size={18} />

                        <span>{item.title}</span>

                      </Link>

                    </SidebarMenuButton>

                  </SidebarMenuItem>
                );
              })}

            </SidebarMenu>

          </SidebarGroupContent>

        </SidebarGroup>

      </SidebarContent>

      <SidebarFooter className="border-t p-4">

        <div>

          <p className="font-semibold">
            Admin
          </p>

          <p className="text-sm text-slate-500">
            Asset Manager
          </p>

        </div>

      </SidebarFooter>

    </Sidebar>
  );
}

export default AppSidebar;