import { Button } from "@/components/ui/button";

const allocations = [
  {
    asset: "Dell Latitude 5420",
    employee: "Rahul",
    department: "IT",
    date: "12 Jul 2026",
    status: "Allocated",
  },
  {
    asset: "HP LaserJet",
    employee: "Amit",
    department: "Finance",
    date: "10 Jul 2026",
    status: "Returned",
  },
];

const statusColor = {
  Allocated: "bg-green-100 text-green-700",
  Returned: "bg-blue-100 text-blue-700",
};

function AllocationTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Asset Allocations
        </h2>

        <Button>Allocate Asset</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left p-4">Asset</th>
            <th className="text-left p-4">Employee</th>
            <th className="text-left p-4">Department</th>
            <th className="text-left p-4">Date</th>
            <th className="text-left p-4">Status</th>
            <th className="text-left p-4">Action</th>

          </tr>

        </thead>

        <tbody>

          {allocations.map((item, index) => (

            <tr key={index} className="border-t">

              <td className="p-4">{item.asset}</td>
              <td className="p-4">{item.employee}</td>
              <td className="p-4">{item.department}</td>
              <td className="p-4">{item.date}</td>

              <td className="p-4">
                <span className={`px-3 py-1 rounded-full text-sm ${statusColor[item.status]}`}>
                  {item.status}
                </span>
              </td>

              <td className="p-4">
                <Button size="sm" variant="outline">
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

export default AllocationTable;