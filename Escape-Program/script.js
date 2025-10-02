// UI Elements
const mainMenuScreen = document.getElementById("main-menu");
const startGameBtn = document.getElementById("start-game-btn");
const quitGameBtn = document.getElementById("quit-game-btn");
const mainMenuMazeBg = document.getElementById("main-menu-maze-bg");

const mazeSizeModal = document.getElementById("maze-size-modal");
const mazeWidthInput = document.getElementById("maze-width");
const mazeHeightInput = document.getElementById("maze-height");
const generateMazeModalBtn = document.getElementById("generate-maze-modal-btn");

const gameScreen = document.getElementById("game-screen");
const gameCanvas = document.getElementById("game-canvas");
const minimapContainer = document.getElementById("minimap-container");
const minimapCanvas = document.getElementById("minimap-canvas");
const pauseButton = document.getElementById("pause-button");

const pauseMenu = document.getElementById("pause-menu");
const resumeGameBtn = document.getElementById("resume-game-btn");
const exitToMainMenuBtn = document.getElementById("exit-to-main-menu-btn");
const solveMazeBtn = document.getElementById("solve-maze-btn");

// Game State
let gameState = "main_menu"; // main_menu, maze_size_prompt, in_game, pause_menu
let mazeGrid = [];
let playerPosition = { x: 0, y: 0 };
let exploredTiles = [];

// Canvas Contexts
const gameCtx = gameCanvas.getContext("2d");
const minimapCtx = minimapCanvas.getContext("2d");
const mainMenuBgCtx = mainMenuMazeBg.getContext("2d");

// Functions to manage screen visibility
function showScreen(screenElement) {
    document.querySelectorAll(".screen").forEach(screen => {
        screen.classList.remove("active");
    });
    screenElement.classList.add("active");
}

function showModal(modalElement) {
    modalElement.classList.add("active");
}

function hideModal(modalElement) {
    modalElement.classList.remove("active");
}

// Event Listeners
startGameBtn.addEventListener("click", () => {
    showModal(mazeSizeModal);
    gameState = "maze_size_prompt";
});

quitGameBtn.addEventListener("click", () => {
    alert("Quitting game... (In a real app, this might close the window or tab)");
});

generateMazeModalBtn.addEventListener("click", () => {
    const width = parseInt(mazeWidthInput.value);
    const height = parseInt(mazeHeightInput.value);

    if (width % 2 === 0 || height % 2 === 0 || width < 5 || width > 51 || height < 5 || height > 51) {
        alert("Please enter odd numbers between 5 and 51 for maze dimensions.");
        return;
    }

    hideModal(mazeSizeModal);
    showScreen(gameScreen);
    gameState = "in_game";
    // TODO: Implement maze generation and game start logic here
    console.log(`Generating maze with dimensions: ${width}x${height}`);
    // Placeholder for actual maze generation and game rendering
    gameCtx.fillStyle = "black";
    gameCtx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
    gameCtx.font = "30px Arial";
    gameCtx.fillStyle = "white";
    gameCtx.textAlign = "center";
    gameCtx.fillText("Maze will be generated here!", gameCanvas.width / 2, gameCanvas.height / 2);
});

pauseButton.addEventListener("click", () => {
    showModal(pauseMenu);
    gameState = "pause_menu";
});

resumeGameBtn.addEventListener("click", () => {
    hideModal(pauseMenu);
    gameState = "in_game";
});

exitToMainMenuBtn.addEventListener("click", () => {
    hideModal(pauseMenu);
    showScreen(mainMenuScreen);
    gameState = "main_menu";
    // TODO: Reset game state
});

solveMazeBtn.addEventListener("click", () => {
    alert("Solving maze... (Feature to be implemented)");
    // TODO: Implement maze solver and path animation
});

// Initial setup
window.addEventListener("resize", () => {
    // Handle canvas resizing if needed, or keep fixed size for game canvas
    // For now, main menu background maze will be responsive
    mainMenuMazeBg.width = window.innerWidth;
    mainMenuMazeBg.height = window.innerHeight;
    // TODO: Re-render main menu background maze
});

// Trigger initial resize to set canvas dimensions
window.dispatchEvent(new Event("resize"));

// Placeholder for main menu background maze animation
function animateMainMenuMazeBg() {
    // This will be replaced with actual maze rendering for background
    mainMenuBgCtx.fillStyle = "#1A1A1D";
    mainMenuBgCtx.fillRect(0, 0, mainMenuMazeBg.width, mainMenuMazeBg.height);
    mainMenuBgCtx.font = "20px Arial";
    mainMenuBgCtx.fillStyle = "rgba(195, 7, 63, 0.1)";
    mainMenuBgCtx.textAlign = "left";
    mainMenuBgCtx.fillText("Background Maze Animation Placeholder", 10, 30);
    requestAnimationFrame(animateMainMenuMazeBg);
}
animateMainMenuMazeBg();

// Game Loop Placeholder (will be expanded later)
function gameLoop() {
    if (gameState === "in_game") {
        // Update game logic (player movement, collisions, etc.)
        // Render game elements on gameCanvas
        // Render minimap on minimapCanvas
    }
    requestAnimationFrame(gameLoop);
}
// gameLoop(); // Start the game loop once game is initialized
