import { Button } from "@/components/ui/button";

const audits = [
  {
    id: "AUD-001",
    department: "IT",
    auditor: "Rahul",
    scheduled: "15 Jul 2026",
    status: "Scheduled",
  },
  {
    id: "AUD-002",
    department: "Finance",
    auditor: "Amit",
    scheduled: "20 Jul 2026",
    status: "In Progress",
  },
  {
    id: "AUD-003",
    department: "HR",
    auditor: "Priya",
    scheduled: "05 Jul 2026",
    status: "Completed",
  },
];

const badge = {
  Scheduled: "bg-yellow-100 text-yellow-700",
  "In Progress": "bg-blue-100 text-blue-700",
  Completed: "bg-green-100 text-green-700",
};

function AuditTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Audit Schedule
        </h2>

        <Button>Create Audit</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left p-4">Audit ID</th>
            <th className="text-left p-4">Department</th>
            <th className="text-left p-4">Auditor</th>
            <th className="text-left p-4">Date</th>
            <th className="text-left p-4">Status</th>
            <th className="text-left p-4">Action</th>

          </tr>

        </thead>

        <tbody>

          {audits.map((audit) => (

            <tr
              key={audit.id}
              className="border-t"
            >

              <td className="p-4">{audit.id}</td>
              <td className="p-4">{audit.department}</td>
              <td className="p-4">{audit.auditor}</td>
              <td className="p-4">{audit.scheduled}</td>

              <td className="p-4">

                <span className={`px-3 py-1 rounded-full text-sm ${badge[audit.status]}`}>
                  {audit.status}
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

export default AuditTable;