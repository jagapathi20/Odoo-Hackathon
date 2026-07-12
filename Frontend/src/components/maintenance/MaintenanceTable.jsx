import { Button } from "@/components/ui/button";

const requests = [
  {
    asset: "Dell Latitude 5420",
    issue: "Screen Flickering",
    technician: "John",
    priority: "High",
    status: "In Progress",
  },
  {
    asset: "Toyota Innova",
    issue: "Oil Change",
    technician: "Mike",
    priority: "Medium",
    status: "Pending",
  },
  {
    asset: "HP LaserJet",
    issue: "Paper Jam",
    technician: "Alex",
    priority: "Low",
    status: "Completed",
  },
];

const statusColor = {
  Pending: "bg-yellow-100 text-yellow-700",
  "In Progress": "bg-blue-100 text-blue-700",
  Completed: "bg-green-100 text-green-700",
};

const priorityColor = {
  High: "bg-red-100 text-red-700",
  Medium: "bg-orange-100 text-orange-700",
  Low: "bg-green-100 text-green-700",
};

function MaintenanceTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Maintenance Requests
        </h2>

        <Button>Create Request</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>
            <th className="text-left p-4">Asset</th>
            <th className="text-left p-4">Issue</th>
            <th className="text-left p-4">Technician</th>
            <th className="text-left p-4">Priority</th>
            <th className="text-left p-4">Status</th>
            <th className="text-left p-4">Action</th>
          </tr>

        </thead>

        <tbody>

          {requests.map((item, index) => (

            <tr key={index} className="border-t">

              <td className="p-4">{item.asset}</td>

              <td className="p-4">{item.issue}</td>

              <td className="p-4">{item.technician}</td>

              <td className="p-4">
                <span className={`px-3 py-1 rounded-full text-sm ${priorityColor[item.priority]}`}>
                  {item.priority}
                </span>
              </td>

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

export default MaintenanceTable;