import { Routes, Route } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import DashboardPage from "../pages/DashboardPage";
import OrgSetupPage from "../pages/OrgSetupPage";
import AssetDirectoryPage from "../pages/AssetDirectoryPage";
import AllocationPage from "../pages/AllocationPage";
import BookingPage from "../pages/BookingPage";
import MaintenancePage from "../pages/MaintenancePage";
import AuditPage from "../pages/AuditPage";
import ReportsPage from "../pages/ReportsPage";
import NotificationsPage from "../pages/NotificationsPage";

import ProtectedRoute from "./ProtectedRoute";

import { ROLES } from "../utils/constants";

function AppRoutes() {
  return (
    <Routes>

      <Route path="/" element={<LoginPage />} />

      <Route
    path="/dashboard"
    element={<DashboardPage />}
    />

      <Route
        path="/organization"
        element={
          <ProtectedRoute
            allowedRoles={[ROLES.ADMIN]}
          >
            <OrgSetupPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/assets"
        element={
          <ProtectedRoute>
            <AssetDirectoryPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/allocations"
        element={
          <ProtectedRoute>
            <AllocationPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/bookings"
        element={
          <ProtectedRoute>
            <BookingPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/maintenance"
        element={
          <ProtectedRoute>
            <MaintenancePage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/audits"
        element={
          <ProtectedRoute>
            <AuditPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/reports"
        element={
          <ProtectedRoute
            allowedRoles={[
              ROLES.ADMIN,
              ROLES.ASSET_MANAGER,
              ROLES.DEPARTMENT_HEAD,
            ]}
          >
            <ReportsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/notifications"
        element={
          <ProtectedRoute>
            <NotificationsPage />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

export default AppRoutes;