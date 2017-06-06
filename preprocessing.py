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
            if event.orderedPitchClasses not in self.chords:
                self.chords.append(event.orderedPitchClasses)
            if octaves not in self.chord_octaves:
                self.chord_octaves.append(octaves)

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
        print(a.chords)
        print(a.chord_octaves)
        print('len(chords): ',len(a.chords))
        print('len(chord_octaves): ',len(a.chord_octaves))
        print('\n')
