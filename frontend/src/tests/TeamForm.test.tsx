import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import TeamForm from "../components/TeamForm";

// Mock the API
vi.mock("../api", () => ({
  teamApi: {
    createTeam: vi.fn(),
  },
}));

import { teamApi } from "../api";
import { Team } from "../types";

describe("TeamForm", () => {
  const mockOnTeamCreated = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders form elements correctly", () => {
    render(<TeamForm onTeamCreated={mockOnTeamCreated} />);

    expect(screen.getByLabelText(/team name/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/enter team name/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /create team/i })
    ).toBeInTheDocument();
  });

  it("shows error when submitting empty form", async () => {
    const user = userEvent.setup();
    render(<TeamForm onTeamCreated={mockOnTeamCreated} />);

    const submitButton = screen.getByRole("button", { name: /create team/i });
    await user.click(submitButton);

    expect(screen.getByText(/team name is required/i)).toBeInTheDocument();
    expect(teamApi.createTeam).not.toHaveBeenCalled();
    expect(mockOnTeamCreated).not.toHaveBeenCalled();
  });

  it("successfully creates a team", async () => {
    const user = userEvent.setup();
    const mockTeam = {
      id: 1,
      team_id: "team-123",
      name: "Test FC",
      created_at: "2024-01-01T10:00:00Z",
    };

    vi.mocked(teamApi.createTeam).mockResolvedValue(mockTeam);

    render(<TeamForm onTeamCreated={mockOnTeamCreated} />);

    const input = screen.getByLabelText(/team name/i);
    const submitButton = screen.getByRole("button", { name: /create team/i });

    await user.type(input, "Test FC");
    await user.click(submitButton);

    expect(teamApi.createTeam).toHaveBeenCalledWith("Test FC");

    await waitFor(() => {
      expect(mockOnTeamCreated).toHaveBeenCalled();
    });

    // Form should be cleared after successful submission
    expect(input).toHaveValue("");
  });

  it("shows error message when API call fails", async () => {
    const user = userEvent.setup();
    const errorMessage = "Failed to create team";

    vi.mocked(teamApi.createTeam).mockRejectedValue(new Error(errorMessage));

    render(<TeamForm onTeamCreated={mockOnTeamCreated} />);

    const input = screen.getByLabelText(/team name/i);
    const submitButton = screen.getByRole("button", { name: /create team/i });

    await user.type(input, "Test FC");
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    expect(mockOnTeamCreated).not.toHaveBeenCalled();
  });

  it("disables form during submission", async () => {
    const user = userEvent.setup();

    // Mock a slow API call
    vi.mocked(teamApi.createTeam).mockImplementation(
      () =>
        new Promise<Team>((resolve) => {
          setTimeout(
            () =>
              resolve({
                id: 1,
                team_id: "team-123",
                name: "Test FC",
                created_at: "2024-01-01T10:00:00Z",
              }),
            100
          );
        })
    );

    render(<TeamForm onTeamCreated={mockOnTeamCreated} />);

    const input = screen.getByLabelText(/team name/i);
    const submitButton = screen.getByRole("button", { name: /create team/i });

    await user.type(input, "Test FC");
    await user.click(submitButton);

    // Should show loading state
    expect(
      screen.getByRole("button", { name: /creating.../i })
    ).toBeInTheDocument();
    expect(input).toBeDisabled();
    expect(submitButton).toBeDisabled();

    // Wait for completion
    await waitFor(() => {
      expect(mockOnTeamCreated).toHaveBeenCalled();
    });
  });
});
