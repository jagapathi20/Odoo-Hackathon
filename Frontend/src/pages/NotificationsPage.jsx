import AppLayout from "@/components/layout/AppLayout";
import NotificationList from "@/components/notifications/NotificationList";

function NotificationsPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Notifications
      </h1>

      <NotificationList />

    </AppLayout>
  );
}

export default NotificationsPage;