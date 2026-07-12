import { Button } from "@/components/ui/button";

const notifications = [
  {
    id: 1,
    title: "Asset Allocation Approved",
    message: "Dell Latitude 5420 has been allocated to Rahul.",
    type: "Success",
    time: "2 mins ago",
  },
  {
    id: 2,
    title: "Maintenance Request",
    message: "Toyota Innova requires servicing.",
    type: "Warning",
    time: "15 mins ago",
  },
  {
    id: 3,
    title: "Booking Reminder",
    message: "Conference Room A booked for 2 PM today.",
    type: "Info",
    time: "1 hour ago",
  },
  {
    id: 4,
    title: "Audit Completed",
    message: "Finance department audit has been completed.",
    type: "Success",
    time: "Yesterday",
  },
];

const colors = {
  Success: "bg-green-100 text-green-700",
  Warning: "bg-yellow-100 text-yellow-700",
  Info: "bg-blue-100 text-blue-700",
};

function NotificationList() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Notifications
        </h2>

        <Button variant="outline">
          Mark all as read
        </Button>

      </div>

      <div className="divide-y">

        {notifications.map((item) => (

          <div
            key={item.id}
            className="flex justify-between items-center p-5"
          >

            <div>

              <h3 className="font-semibold">
                {item.title}
              </h3>

              <p className="text-gray-500 mt-1">
                {item.message}
              </p>

              <p className="text-sm text-gray-400 mt-2">
                {item.time}
              </p>

            </div>

            <span
              className={`px-3 py-1 rounded-full text-sm ${colors[item.type]}`}
            >
              {item.type}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}

export default NotificationList;