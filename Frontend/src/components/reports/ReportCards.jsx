function ReportCards() {
  const cards = [
    {
      title: "Total Assets",
      value: "245",
      color: "text-blue-600",
    },
    {
      title: "Assets Allocated",
      value: "181",
      color: "text-green-600",
    },
    {
      title: "Under Maintenance",
      value: "12",
      color: "text-red-600",
    },
    {
      title: "Utilization",
      value: "74%",
      color: "text-yellow-500",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

      {cards.map((card) => (

        <div
          key={card.title}
          className="bg-white border rounded-xl shadow-sm p-6"
        >

          <p className="text-gray-500">
            {card.title}
          </p>

          <h2 className={`text-4xl font-bold mt-3 ${card.color}`}>
            {card.value}
          </h2>

        </div>

      ))}

    </div>
  );
}

export default ReportCards;