import { Button } from "@/components/ui/button";

const employees = [
  {
    id: 1,
    name: "Rahul",
    department: "IT",
    role: "Admin",
  },
  {
    id: 2,
    name: "Amit",
    department: "Finance",
    role: "Employee",
  },
  {
    id: 3,
    name: "Priya",
    department: "HR",
    role: "Department Head",
  },
];

function EmployeeTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Employees
        </h2>

        <Button>Add Employee</Button>

      </div>

      <table className="w-full">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left p-4">Name</th>

            <th className="text-left p-4">Department</th>

            <th className="text-left p-4">Role</th>

            <th className="text-left p-4">Action</th>

          </tr>

        </thead>

        <tbody>

          {employees.map((emp) => (

            <tr
              key={emp.id}
              className="border-t"
            >

              <td className="p-4">{emp.name}</td>

              <td className="p-4">{emp.department}</td>

              <td className="p-4">{emp.role}</td>

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

export default EmployeeTable;