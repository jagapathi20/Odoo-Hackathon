import AppLayout from "@/components/layout/AppLayout";
import BookingTable from "@/components/bookings/BookingTable";

function BookingPage() {
  return (
    <AppLayout>

      <h1 className="text-3xl font-bold mb-8">
        Resource Bookings
      </h1>

      <BookingTable />

    </AppLayout>
  );
}

export default BookingPage;