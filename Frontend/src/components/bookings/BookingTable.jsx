import { Button } from "@/components/ui/button";

const bookings = [
  {
    resource: "Conference Room A",
    employee: "Rahul",
    date: "13 Jul 2026",
    time: "09:00 - 11:00",
    status: "Approved",
  },
  {
    resource: "Toyota Innova",
    employee: "Amit",
    date: "14 Jul 2026",
    time: "02:00 - 04:00",
    status: "Pending",
  },
];

const badge = {
  Approved: "bg-green-100 text-green-700",
  Pending: "bg-yellow-100 text-yellow-700",
};

function BookingTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Resource Bookings
        </h2>

        <Button>New Booking</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left p-4">Resource</th>
            <th className="text-left p-4">Employee</th>
            <th className="text-left p-4">Date</th>
            <th className="text-left p-4">Time</th>
            <th className="text-left p-4">Status</th>
            <th className="text-left p-4">Action</th>

          </tr>

        </thead>

        <tbody>

          {bookings.map((booking, index) => (

            <tr key={index} className="border-t">

              <td className="p-4">{booking.resource}</td>

              <td className="p-4">{booking.employee}</td>

              <td className="p-4">{booking.date}</td>

              <td className="p-4">{booking.time}</td>

              <td className="p-4">

                <span className={`px-3 py-1 rounded-full text-sm ${badge[booking.status]}`}>
                  {booking.status}
                </span>

              </td>

              <td className="p-4">

                <Button
                  size="sm"
                  variant="outline"
                >
                  View
                </Button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default BookingTable;