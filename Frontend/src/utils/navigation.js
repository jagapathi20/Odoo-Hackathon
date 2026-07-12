import {
  LayoutDashboard,
  Building2,
  Boxes,
  ClipboardList,
  CalendarDays,
  Wrench,
  ClipboardCheck,
  BarChart3,
  Bell,
} from "lucide-react";

import { ROLES } from "./constants";

export const navigation = [
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
      ROLES.EMPLOYEE,
    ],
  },

  {
    title: "Organization",
    path: "/organization",
    icon: Building2,
    roles: [ROLES.ADMIN],
  },

  {
    title: "Assets",
    path: "/assets",
    icon: Boxes,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
      ROLES.EMPLOYEE,
    ],
  },

  {
    title: "Allocations",
    path: "/allocations",
    icon: ClipboardList,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
    ],
  },

  {
    title: "Bookings",
    path: "/bookings",
    icon: CalendarDays,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
      ROLES.EMPLOYEE,
    ],
  },

  {
    title: "Maintenance",
    path: "/maintenance",
    icon: Wrench,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
      ROLES.EMPLOYEE,
    ],
  },

  {
    title: "Audits",
    path: "/audits",
    icon: ClipboardCheck,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
    ],
  },

  {
    title: "Reports",
    path: "/reports",
    icon: BarChart3,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
    ],
  },

  {
    title: "Notifications",
    path: "/notifications",
    icon: Bell,
    roles: [
      ROLES.ADMIN,
      ROLES.ASSET_MANAGER,
      ROLES.DEPARTMENT_HEAD,
      ROLES.EMPLOYEE,
    ],
  },
];