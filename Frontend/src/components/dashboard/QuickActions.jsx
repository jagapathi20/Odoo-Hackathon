import { Button } from "@/components/ui/button";

function QuickActions() {
  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">

      <h2 className="font-semibold text-lg mb-5">
        Quick Actions
      </h2>

      <div className="grid gap-3">

        <Button>Add Asset</Button>

        <Button variant="outline">
          Allocate Asset
        </Button>

        <Button variant="outline">
          Create Booking
        </Button>

        <Button variant="outline">
          Generate Report
        </Button>

      </div>

    </div>
  );
}

export default QuickActions;