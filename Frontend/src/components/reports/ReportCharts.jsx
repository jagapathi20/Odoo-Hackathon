function ReportCharts() {
  const data = [35, 60, 45, 80, 55, 95, 70];

  return (
    <div className="grid lg:grid-cols-2 gap-6 mt-8">

      <div className="bg-white rounded-xl border shadow-sm p-6">

        <h2 className="text-xl font-semibold mb-6">
          Asset Growth
        </h2>

        <div className="flex items-end gap-3 h-56">

          {data.map((height, index) => (

            <div
              key={index}
              className="flex-1 bg-blue-500 rounded-t-lg"
              style={{
                height: `${height}%`,
              }}
            />

          ))}

        </div>

      </div>

      <div className="bg-white rounded-xl border shadow-sm p-6">

        <h2 className="text-xl font-semibold mb-6">
          Asset Status
        </h2>

        <div className="space-y-5">

          <div>

            <div className="flex justify-between">

              <span>Allocated</span>

              <span>74%</span>

            </div>

            <div className="h-3 bg-gray-200 rounded-full mt-2">

              <div className="bg-blue-500 h-3 rounded-full w-3/4"/>

            </div>

          </div>

          <div>

            <div className="flex justify-between">

              <span>Available</span>

              <span>18%</span>

            </div>

            <div className="h-3 bg-gray-200 rounded-full mt-2">

              <div
                className="bg-green-500 h-3 rounded-full"
                style={{ width: "18%" }}
              />

            </div>

          </div>

          <div>

            <div className="flex justify-between">

              <span>Maintenance</span>

              <span>8%</span>

            </div>

            <div className="h-3 bg-gray-200 rounded-full mt-2">

              <div
                className="bg-red-500 h-3 rounded-full"
                style={{ width: "8%" }}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default ReportCharts;