import { Routes, Route, Link, useLocation } from "react-router-dom";
import Teams from "./pages/Teams";
import Tournaments from "./pages/Tournaments";

function App() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between">
            <div className="flex items-center">
              <div className="shrink-0">
                <h1 className="text-xl font-bold text-gray-900">
                  Football Tournament Manager
                </h1>
              </div>
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to="/teams"
                  className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    location.pathname === "/teams" || location.pathname === "/"
                      ? "bg-blue-100 text-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
                >
                  Teams
                </Link>
                <Link
                  to="/tournaments"
                  className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    location.pathname === "/tournaments"
                      ? "bg-green-100 text-green-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
                >
                  Tournaments
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <Routes>
            <Route path="/" element={<Teams />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/tournaments" element={<Tournaments />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default App;
