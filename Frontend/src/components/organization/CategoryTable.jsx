import { Button } from "@/components/ui/button";

const categories = [
  "Laptop",
  "Desktop",
  "Printer",
  "Projector",
  "Vehicle",
];

function CategoryTable() {
  return (
    <div className="bg-white rounded-xl border shadow-sm">

      <div className="flex justify-between items-center p-5 border-b">

        <h2 className="text-xl font-semibold">
          Categories
        </h2>

        <Button>Add Category</Button>

      </div>

      <div className="p-5 space-y-3">

        {categories.map((cat) => (

          <div
            key={cat}
            className="flex justify-between items-center border rounded-lg p-3"
          >

            <span>{cat}</span>

            <Button
              variant="outline"
              size="sm"
            >
              Edit
            </Button>

          </div>

        ))}

      </div>

    </div>
  );
}

export default CategoryTable;