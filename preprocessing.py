from music21 import *
import os


def load_data(file_path):
    pre_piece = converter.parse(file_path)
    k = pre_piece.analyze('key')
    if k.mode == 'minor':
        i = interval.Interval(k.parallel.tonic, pitch.Pitch('C'))
    else:
        i = interval.Interval(k.tonic, pitch.Pitch('C'))
    piece = pre_piece.transpose(i)
    # print(file_path)
    return piece

class preprocessing(object):
    def __init__(self):
        self.chords = []
        self.chord_octaves = []
        self.chord_ref = [[0, 4, 7], [2, 7, 11], [2, 5, 10], [0, 5, 9], [3, 7, 10], [0, 5, 8], [1, 5, 10], [2, 5, 9], [0, 4, 9],
         [2, 7, 10], [2, 11], [0, 4], [2, 5], [0, 4, 7, 10], [2, 6, 9], [4, 7], [0, 5], [5, 11], [5, 9], [2, 4], [5, 7],
         [0, 3, 7], [0, 2, 6, 9], [1, 4, 7, 9], [2, 5, 7, 11], [1, 4, 7], [1, 5, 8], [1, 4, 9], [4, 8, 11], [7, 11],
         [0, 9], [4, 8], [0, 7, 9], [2, 7], [4, 7, 11], [3, 6, 11], [0, 3], [3, 7], [5, 8], [2, 10], [7, 10], [0, 8],
         [5, 10], [0, 3, 8], [2, 5, 8, 10], [2, 5, 11], [0, 2, 5, 8], [3, 6, 10], [0, 3, 5, 9], [6, 9], [2, 4, 8, 11],
         [5, 8, 11], [0, 2, 5, 9], [1, 6], [5, 7, 11], [4, 7, 9], [1, 3, 7, 10], [0, 4, 7, 9], [0, 6, 9], [2, 5, 7, 10],
         [1, 6, 10], [1, 4, 6, 10], [3, 6, 9, 11], [2, 6, 11], [0, 7], [0, 3, 6, 8], [1, 6, 9], [3, 6], [3, 10],
         [0, 3, 5, 8], [0, 2], [2], [3, 9], [3], [0, 3, 6]]
        self.octave_ref = [[3, 3, 3], [2, 3, 2], [3, 2, 3], [3, 4, 3], [4, 3, 4], [5, 4], [5, 5], [3, 3, 3, 3], [4, 4], [3, 3, 4, 3],
         [4, 3, 4, 4], [4, 4, 3, 3], [4, 3], [4, 4, 4], [2, 2, 2], [3, 3, 2, 2], [4, 5], [4, 4, 4, 4], [3, 2, 3, 3],
         [2, 2], [3, 3], [3, 4, 4], [4, 3, 3], [4, 4, 3], [2, 3, 3], [4, 4, 4, 3], [4, 5, 4], [5, 4, 4, 4],
         [2, 2, 3, 2], [3, 4, 3, 4]]

        self.chords_cnt = [0] * len(self.chord_ref)
        self.chord_octaves_cnt = [0] * len(self.octave_ref)

    def streaming(self, part, event, part_tuples):
        # save start time
        for y in event.contextSites():
            if y[0] is part:
                offset=y[1]
        # if current event is chord
        if getattr(event, 'isChord', None) and event.isChord:
            # chord pitch wjdfl
            octaves = []
            for pitch in event.pitches:
                octaves.append(pitch.octave)
            # save index for sorting pitches of chord
            sort_idx = [i[0] for i in sorted(enumerate(event.pitchClasses), key=lambda x: x[1])]
            octaves = [x for (y, x) in sorted(zip(sort_idx, octaves))]

            ch_idx = self.chord_ref.index(event.orderedPitchClasses)
            oc_idx = self.octave_ref.index(octaves)
            self.chords_cnt[ch_idx] += 1
            self.chord_octaves_cnt[oc_idx] += 1
            """
            if event.orderedPitchClasses not in self.chords:
                self.chords.append(event.orderedPitchClasses)
            if octaves not in self.chord_octaves:
                self.chord_octaves.append(octaves)

            """

            for note in event._notes:
                part_tuples.append([offset, note.quarterLength, note.pitch.octave, note.pitch.name, note.volume.velocity])
        # if current event is note
        if getattr(event, 'isNote', None) and event.isNote:
            # change to key
            # make one step in sequence
            part_tuples.append([offset, event.quarterLength, event.pitch.octave, event.pitch.name, event.volume.velocity])
        # if current event is rest
        if getattr(event, 'isRest', None) and event.isRest:
            part_tuples.append([offset, event.quarterLength, 'Rest', 'Rest', 0])
        return part_tuples

    def parsing(self, data_path):
        piece = load_data(data_path)
        all_parts=[]
        for part in piece.iter.activeElementList:
            """
            try:
                track_name = part[0].bestName()
            except AttributeError:
                track_name = 'None'
            part_tuples.append(track_name)
            
            """
            part_tuples = []
            for event in part._elements:
                # if Chord or Notes exist recursive
                if event.isStream :
                    _part_tuples = []
                    for i in event._elements:
                        _part_tuples = self.streaming(event, i, _part_tuples)
                    all_parts.append(_part_tuples)
                # normal case
                else:
                    part_tuples = self.streaming(part, event, part_tuples)
            if part_tuples != []:
                all_parts.append(part_tuples)
        print(piece.analyze('key'))
        return all_parts




if __name__ == "__main__":
    a = preprocessing()
    for file in os.listdir('./Nottingham/all'):
        all_parts = a.parsing('./Nottingham/all/'+file)
        print(file)
        print('chords_cnt: ', a.chords_cnt)
        print('octaves_cnt: ', a.chord_octaves_cnt)
        """
        print(a.chords)
        print(a.chord_octaves)
        print('len(chords): ',len(a.chords))
        print('len(chord_octaves): ',len(a.chord_octaves))
        """
        print('\n')
