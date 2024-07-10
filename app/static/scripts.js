var caretPosition = 0;

async function tokenizeText() {
  try {
    var inputText = document.getElementById("inputText");
    caretPosition = getCaretPosition(inputText);
    var text = inputText.textContent;
    //text = text.toLowerCase();
    // Send the input text to the server for tokenization
    const tokenizeResponse = await fetch("/tokenize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
      }),
    });
    const tokenizeData = await tokenizeResponse.json();
    console.log("Returned Tokens:", tokenizeData.tokens);

    // Detect errors
    const detectErrorsResponse = await fetch("/detect_errors", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tokens: tokenizeData.tokens,
      }),
    });
    const detectErrorsData = await detectErrorsResponse.json();
    console.log("Errors:", detectErrorsData.errors);
    console.log("error_classes:", detectErrorsData.error_classes);

    // Correct errors and generate suggestions for each error
    let allSuggestions = {};

    // Assuming detectErrorsData.errors is an object with error codes as keys
    for (let error_class of Object.keys(detectErrorsData.error_classes)) {
      const errorDetails = detectErrorsData.error_classes[error_class]; // Assuming errorDetails is the dictionary containing error details

      // Assuming errorDetails is a dictionary containing additional error information
      const correctErrorsResponse = await fetch("/correct_errors", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          error_class: error_class,
          details: errorDetails // Sending error details along with error code
        }),
      });

      const correctErrorsData = await correctErrorsResponse.json();
      console.log("Returned Corrections:", correctErrorsData.corrections);

      // Generate words
      const generateWordsResponse = await fetch("/generate_words", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          morphemes: correctErrorsData.corrections,
          error_class: error_class,

        }),
      });
      const generateWordsData = await generateWordsResponse.json();
      console.log("Generated Words:", generateWordsData.words);
      allSuggestions[error_class] = generateWordsData.words;
    }

    // Apply styling with ranked suggestions
    applyErrorStyling(detectErrorsData.errors, allSuggestions);

    // Handle the server response for ranked suggestions if needed
    console.log("Ranked Suggestions:", allSuggestions);
  } catch (error) {
    console.error("Error:", error);
  }
}

function applyErrorStyling(errors, suggestions) {
  var inputTextContainer = document.getElementById("inputText");
  var pattern = /(\b[\w\'-]+(?:[.,;:!?\"'])?\b|\d+|[.,;:!?()\"'\s])/g;
  //inputTextContainer =  inputTextContainer.toLowerCase();
  var words = inputTextContainer.textContent.match(pattern);
  //words = words.toLowerCase();
  inputTextContainer.innerHTML = "";

  words.forEach((word) => {
    var span = document.createElement("span");
    span.textContent = word;
    var trimmedWord = word.trim().toLowerCase();
    if (errors.hasOwnProperty(trimmedWord) && errors[trimmedWord] === false) {
      span.classList.add("misspelled");
      span.onclick = function () {
        var wordSuggestions = suggestions[trimmedWord];
        displaySuggestions(wordSuggestions, trimmedWord, span);
      };
    }
    inputTextContainer.appendChild(span);
  });

  setCaretPosition(inputTextContainer);
}

function displaySuggestions(suggestions, misspelledWord, misspelledSpan) {
  var suggestionsContainer = document.getElementById("suggestions");
  suggestionsContainer.innerHTML = ""; // Clear previous suggestions

  // Limit the number of suggestions
  var maxSuggestions = 15;
  suggestions = suggestions.slice(0, maxSuggestions);

  suggestions.forEach((suggestion) => {
    var listItem = document.createElement("li");
    listItem.textContent = suggestion;
    listItem.onclick = function () {
      replaceMisspelledWord(misspelledWord, suggestion);
      misspelledSpan.classList.remove("misspelled");
      suggestionsContainer.innerHTML = ""; // Clear suggestions after selecting one
      suggestionsContainer.style.display = "none"; // Hide the suggestions container
    };
    suggestionsContainer.appendChild(listItem);
  });

  // Create a new div for the icons
  var iconsDiv = document.createElement("div");
  iconsDiv.id = "suggestion-actions";
  iconsDiv.style.display = "flex";
  iconsDiv.style.justifyContent = "space-between";

  // Create the left icon and add the hover text
  var leftIcon = document.createElement("i");
  leftIcon.className = "bi bi-slash-circle"; // Use Bootstrap icon class
  leftIcon.title = "Ignore All";

  leftIcon.onclick = function () {
    fetch("/add_to_ignored_words", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        word: misspelledWord,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Added error word to ignored words:", data.message);
      });
    suggestionsContainer.style.display = "none";
    misspelledSpan.classList.remove("misspelled");
  };
  iconsDiv.appendChild(leftIcon);

  // Create the right icon and add the hover text
  var rightIcon = document.createElement("i");
  rightIcon.className = "bi bi-file-earmark-plus"; // Use Bootstrap icon class
  rightIcon.title = "Add to Dictionary";

  rightIcon.onclick = function () {
    fetch("/add_to_custom_dictionary", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        word: misspelledWord,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(
          "Added error word to custom dictionary words:",
          data.message
        );
      });
    suggestionsContainer.style.display = "none";
    misspelledSpan.classList.remove("misspelled");
  };
  iconsDiv.appendChild(rightIcon);

  // Add the icons div to the suggestions container
  suggestionsContainer.appendChild(iconsDiv);

  // Position the suggestions container below the misspelled word
  var rect = misspelledSpan.getBoundingClientRect();
  suggestionsContainer.style.top = rect.bottom + "px";
  suggestionsContainer.style.left = rect.left + "px";

  // Show the suggestions container
  suggestionsContainer.style.display = "block";
}

function replaceMisspelledWord(misspelledWord, suggestion) {
  const inputTextContainer = document.getElementById("inputText");
  const text = inputTextContainer.textContent;

  const range = document.createRange();
  range.selectNodeContents(inputTextContainer);

  const walker = document.createTreeWalker(
    inputTextContainer,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  let currentNode;

  while ((currentNode = walker.nextNode())) {
    const index = currentNode.textContent.indexOf(misspelledWord);

    if (index !== -1) {
      range.setStart(currentNode, index);
      range.setEnd(currentNode, index + misspelledWord.length);
      range.deleteContents();
      range.insertNode(document.createTextNode(suggestion));
      break;
    }
  }
}

function handlePaste(e) {
  e.preventDefault();
  var text = (e.originalEvent || e).clipboardData.getData("text/plain");
  document.execCommand("insertText", false, text);
}

function handleDrop(e) {
  e.preventDefault();
  var text = e.dataTransfer.getData("text");
  var selection = window.getSelection();
  if (!selection.rangeCount) return false;
  selection.deleteFromDocument();
  selection.getRangeAt(0).insertNode(document.createTextNode(text));
}

function getCaretPosition(editableDiv) {
  var caretPos = 0,
    sel,
    range;
  if (window.getSelection) {
    sel = window.getSelection();
    if (sel.rangeCount) {
      range = sel.getRangeAt(0);
      if (range.commonAncestorContainer.parentNode === editableDiv) {
        caretPos = range.endOffset;
      }
    }
  } else if (document.selection && document.selection.createRange) {
    range = document.selection.createRange();
    if (range.parentElement() === editableDiv) {
      var tempEl = document.createElement("span");
      editableDiv.insertBefore(tempEl, editableDiv.firstChild);
      var tempRange = range.duplicate();
      tempRange.moveToElementText(tempEl);
      tempRange.setEndPoint("EndToEnd", range);
      caretPos = tempRange.text.length;
    }
  }
  return caretPos;
}

function setCaretPosition(editableDiv) {
  var range = document.createRange();
  var sel = window.getSelection();
  range.selectNodeContents(editableDiv);
  range.collapse(false);
  sel.removeAllRanges();
  sel.addRange(range);
}

function handleInput(event) {
  var char = event.data;
  if (
    char === " " ||
    char === "." ||
    char === "," ||
    char === "!" ||
    char === "?"
  ) {
    tokenizeText();
  }
}

// Hide the suggestions container when clicking outside
document.addEventListener("click", function (event) {
  var inputTextContainer = document.getElementById("inputText");
  var suggestionsContainer = document.getElementById("suggestions");
  if (
    !inputTextContainer.contains(event.target) &&
    !suggestionsContainer.contains(event.target)
  ) {
    suggestionsContainer.style.display = "none";
  }
});


//theming
document.addEventListener('DOMContentLoaded', function() {
  const themeToggleCheckbox = document.getElementById('theme-toggle-checkbox');

  themeToggleCheckbox.addEventListener('change', function() {
      document.body.classList.toggle('dark-theme');
      document.getElementById('body').classList.toggle('dark-theme');
  });
});



function updateYear() {
  var currentYear = new Date().getFullYear();
  document.getElementById("currentYear").textContent = currentYear;
}

// Call the function initially to display the current year
updateYear();
function handlePlaceholder() {
  var inputTextContainer = document.getElementById("inputText");
  var placeholder = inputTextContainer.getAttribute("data-text");
  
  // Check if the text area is empty
  if (!inputTextContainer.textContent.trim()) {
    inputTextContainer.textContent = placeholder;
  }
}

// Call the function initially to set the placeholder text
handlePlaceholder();