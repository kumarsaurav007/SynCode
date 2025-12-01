import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface EditorState {
  code: string;
  suggestion: string;
}

const initialState: EditorState = {
  code: "",
  suggestion: ""
};

const editorSlice = createSlice({
  name: "editor",
  initialState,
  reducers: {
    setCode(state, action: PayloadAction<string>) {
      state.code = action.payload;
    },
    setSuggestion(state, action: PayloadAction<string>) {
      state.suggestion = action.payload;
    },
    clearSuggestion(state) {
      state.suggestion = "";
    }
  }
});

export const { setCode, setSuggestion, clearSuggestion } = editorSlice.actions;
export default editorSlice.reducer;
