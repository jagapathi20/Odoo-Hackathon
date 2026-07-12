import { Button } from "@/components/ui/button";

const departments = [
  { id: 1, name: "IT", head: "Rahul", employees: 12 },
  { id: 2, name: "Finance", head: "Amit", employees: 8 },
  { id: 3, name: "HR", head: "Priya", employees: 5 },
];

function DepartmentTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Departments
        </h2>

        <Button>Add Department</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left p-4">Department</th>

            <th className="text-left p-4">Head</th>

            <th className="text-left p-4">Employees</th>

            <th className="text-left p-4">Action</th>

          </tr>

        </thead>

        <tbody>

          {departments.map((dept) => (

            <tr
              key={dept.id}
              className="border-t"
            >

              <td className="p-4">{dept.name}</td>

              <td className="p-4">{dept.head}</td>

              <td className="p-4">{dept.employees}</td>

              <td className="p-4">

                <Button
                  variant="outline"
                  size="sm"
                >
                  Edit
                </Button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default DepartmentTable;