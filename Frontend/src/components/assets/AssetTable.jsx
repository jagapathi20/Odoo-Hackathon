import { Button } from "@/components/ui/button";

const assets = [
  {
    id: "AST-001",
    name: "Dell Latitude 5420",
    category: "Laptop",
    department: "IT",
    status: "Available",
  },
  {
    id: "AST-002",
    name: "HP LaserJet M404",
    category: "Printer",
    department: "Admin",
    status: "Allocated",
  },
  {
    id: "AST-003",
    name: "Toyota Innova",
    category: "Vehicle",
    department: "Transport",
    status: "Maintenance",
  },
];

const badge = {
  Available: "bg-green-100 text-green-700",
  Allocated: "bg-blue-100 text-blue-700",
  Maintenance: "bg-red-100 text-red-700",
};

function AssetTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Asset Directory
        </h2>

        <Button>Add Asset</Button>

      </div>

      <div className="p-5">

        <input
          placeholder="Search asset..."
          className="w-full border rounded-lg px-4 py-3 mb-5"
        />

        <table className="w-full">

          <thead className="bg-gray-50">

            <tr>

              <th className="text-left p-4">ID</th>
              <th className="text-left p-4">Asset</th>
              <th className="text-left p-4">Category</th>
              <th className="text-left p-4">Department</th>
              <th className="text-left p-4">Status</th>
              <th className="text-left p-4">Action</th>

            </tr>

          </thead>

          <tbody>

            {assets.map((asset) => (

              <tr key={asset.id} className="border-t">

                <td className="p-4">{asset.id}</td>

                <td className="p-4">{asset.name}</td>

                <td className="p-4">{asset.category}</td>

                <td className="p-4">{asset.department}</td>

                <td className="p-4">

                  <span
                    className={`px-3 py-1 rounded-full text-sm ${badge[asset.status]}`}
                  >
                    {asset.status}
                  </span>

                </td>

                <td className="p-4">

                  <Button
                    variant="outline"
                    size="sm"
                  >
                    View
                  </Button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default AssetTable;