function RecentActivity() {
  const activities = [
    "Laptop allocated to Rahul",
    "Vehicle booking approved",
    "Printer sent for maintenance",
    "Audit scheduled",
    "Fuel request approved",
  ];

  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">

      <h2 className="font-semibold text-lg mb-5">
        Recent Activity
      </h2>

      <div className="space-y-4">

        {activities.map((item, index) => (
          <div
            key={index}
            className="border-b pb-3 last:border-none"
          >
            {item}
          </div>
        ))}

      </div>

    </div>
  );
}

export default RecentActivity;
